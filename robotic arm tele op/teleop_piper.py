import time
import cv2
import math
import numpy as np
from scipy.spatial.transform import Rotation as R_scipy
from webcam_aruco_tracker import WebcamArucoTracker
from piper_sdk import C_PiperInterface_V2

def clip_pose_mm(x, y, z):
    """
    Clamps coordinates (in mm) to a safe workspace bounding box.
    Prevents the IK solver from crashing into the physical table or its own base.
    """
    x = np.clip(x, 150, 400)   # X: Forward/Backward (mm)
    y = np.clip(y, -250, 250)  # Y: Left/Right (mm)
    z = np.clip(z, 50, 350)    # Z: Up/Down (mm)
    return x, y, z

def main():
    print("Initializing Piper-X Arm on can0...")
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    
    print("Enabling arm (waiting for ready)...")
    while not piper.EnablePiper():
        time.sleep(0.01)
    print("Arm Enabled and Holding Position.")

    # Initialize gripper
    piper.GripperCtrl(0, 1000, 0x01, 0)

    print("Starting Webcam Tracker...")
    # 5 markers tracked, edge length 0.06m (6cm)
    tracker = WebcamArucoTracker(marker_length=0.06, alpha=0.65, camera_index=0)
    tracker.start()
    
    print("\n=== SYSTEM READY ===")
    print("1. Manually move the physical arm near the center of your desk.")
    print("2. Hold the object with ArUco markers in the camera view.")
    print("3. Press 'o' in the video window to lock origin and begin tracking.")
    print("4. Press SPACE or 'c' to toggle the gripper (Open / Soft Close).")
    print("5. Press 's' to pause movement. Press 'q' to quit.\n")
    
    is_active = False
    origin_pose = None
    origin_rotation_matrix = None
    origin_R_scipy = None
    R_home_scipy = None
    error_printed = False
    gripper_is_open = False  # Starts closed

    # Teleoperation Sensitivity & Inversion Scales
    # Set to -1.0 if any axis is inverted relative to your perspective
    POS_SCALE_X = 1.0   # Forward (+) / Backward (-)
    POS_SCALE_Y = 1.0   # Left (+) / Right (-)
    POS_SCALE_Z = 1.0   # Up (+) / Down (-)
    ROT_SCALE = 1.0     # 1:1 rotation mapping

    # Robot home position based on actual safe pose
    ROBOT_HOME_X_MM = 287.8    # Forward (mm)
    ROBOT_HOME_Y_MM = 17.9     # Left/Right (mm)
    ROBOT_HOME_Z_MM = 287.6    # Up (mm)
    ROBOT_HOME_RX_DEG = -90.4  # Roll (degrees)
    ROBOT_HOME_RY_DEG = 9.9    # Pitch (degrees)
    ROBOT_HOME_RZ_DEG = -92.5  # Yaw (degrees)

    # SDK unit factor: positions in 0.001mm, angles in 0.001deg
    FACTOR = 1000

    # Exponential Moving Average state for smoothing coordinates
    # 0.35 provides crisp, real-time response while filtering out high-frequency tremor
    ema_alpha = 0.35
    ema_target = None

    try:
        while True:
            start_time = time.time()
            positions, frame = tracker.step()
            
            # Handle Keyboard Toggles
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('o'):
                if positions and positions.get(0) is not None and tracker.rotation_matrix is not None:
                    # 1. Capture Camera Origin
                    origin_pose = positions[0].copy()
                    origin_rotation_matrix = tracker.rotation_matrix.copy()
                    origin_R_scipy = R_scipy.from_matrix(origin_rotation_matrix)
                    
                    # 2. Capture Robot's Current Physical Pose as the new Home
                    current_robot_pose = piper.GetArmEndPoseMsgs()
                    ROBOT_HOME_X_MM = current_robot_pose.end_pose.X_axis / 1000.0
                    ROBOT_HOME_Y_MM = current_robot_pose.end_pose.Y_axis / 1000.0
                    ROBOT_HOME_Z_MM = current_robot_pose.end_pose.Z_axis / 1000.0
                    ROBOT_HOME_RX_DEG = current_robot_pose.end_pose.RX_axis / 1000.0
                    ROBOT_HOME_RY_DEG = current_robot_pose.end_pose.RY_axis / 1000.0
                    ROBOT_HOME_RZ_DEG = current_robot_pose.end_pose.RZ_axis / 1000.0
                    R_home_scipy = R_scipy.from_euler('xyz', [ROBOT_HOME_RX_DEG, ROBOT_HOME_RY_DEG, ROBOT_HOME_RZ_DEG], degrees=True)
                    
                    is_active = True
                    error_printed = False
                    ema_target = None  # Reset smoothing on new origin
                    print(f"\n>>> Origin locked! Robot Home dynamically set to: X={ROBOT_HOME_X_MM:.1f}mm, Y={ROBOT_HOME_Y_MM:.1f}mm, Z={ROBOT_HOME_Z_MM:.1f}mm <<<")
                    print("Teleoperation ACTIVE.")
                else:
                    print("Cannot set origin: ArUco markers not currently visible.")
            elif key == ord('s'):
                is_active = False
                print("Teleoperation PAUSED.")
            elif key == ord('c') or key == ord(' '):  # Toggle with 'c' or SPACEBAR
                gripper_is_open = not gripper_is_open
                if gripper_is_open:
                    print("\n>>> Gripper: OPENING (70mm) <<<")
                    # Open to 70mm, normal torque
                    piper.GripperCtrl(70000, 1000, 0x01, 0)
                else:
                    print("\n>>> Gripper: SOFT CLOSING (Grasping, 0mm @ 0.8 N.m) <<<")
                    # Close to 0mm, limit torque to 800 (0.8 N.m) to grip without crushing
                    piper.GripperCtrl(0, 800, 0x01, 0)
            
            if frame is not None:
                if positions and positions.get(0) is not None:
                    current_raw_pose = positions[0]
                    
                    if is_active and origin_pose is not None and origin_R_scipy is not None and R_home_scipy is not None:
                        # Position delta from captured origin (meters -> mm with directional scaling)
                        dx_mm = (current_raw_pose[0] - origin_pose[0]) * 1000.0 * POS_SCALE_X
                        dy_mm = (current_raw_pose[1] - origin_pose[1]) * 1000.0 * POS_SCALE_Y
                        dz_mm = (current_raw_pose[2] - origin_pose[2]) * 1000.0 * POS_SCALE_Z
                        
                        # True 3D SO(3) rotation delta (eliminates gimbal lock and axis swapping)
                        if tracker.rotation_matrix is not None:
                            R_curr_scipy = R_scipy.from_matrix(tracker.rotation_matrix)
                            R_delta = R_curr_scipy * origin_R_scipy.inv()
                            
                            if ROT_SCALE != 1.0:
                                rotvec = R_delta.as_rotvec() * ROT_SCALE
                                R_delta = R_scipy.from_rotvec(rotvec)
                                
                            R_target = R_delta * R_home_scipy
                            target_rx_deg, target_ry_deg, target_rz_deg = R_target.as_euler('xyz', degrees=True)
                        else:
                            target_rx_deg, target_ry_deg, target_rz_deg = ROBOT_HOME_RX_DEG, ROBOT_HOME_RY_DEG, ROBOT_HOME_RZ_DEG
                        
                        # Apply delta to the robot's home position (in mm)
                        target_x_mm = ROBOT_HOME_X_MM + dx_mm
                        target_y_mm = ROBOT_HOME_Y_MM + dy_mm
                        target_z_mm = ROBOT_HOME_Z_MM + dz_mm
                        
                        # Enforce the safety bounding box (in mm)
                        target_x_mm, target_y_mm, target_z_mm = clip_pose_mm(
                            target_x_mm, target_y_mm, target_z_mm
                        )

                        # Apply Exponential Moving Average (EMA) to smooth out hand jitter
                        current_target = np.array([
                            target_x_mm, target_y_mm, target_z_mm,
                            target_rx_deg, target_ry_deg, target_rz_deg
                        ])
                        
                        if ema_target is None:
                            ema_target = current_target
                        else:
                            ema_target = ema_alpha * current_target + (1.0 - ema_alpha) * ema_target
                            
                        sm_x, sm_y, sm_z, sm_rx, sm_ry, sm_rz = ema_target
                        
                        # Convert smoothed targets to SDK units: mm * 1000 and deg * 1000
                        x_sdk = round(sm_x * FACTOR)
                        y_sdk = round(sm_y * FACTOR)
                        z_sdk = round(sm_z * FACTOR)
                        rx_sdk = round(sm_rx * FACTOR)
                        ry_sdk = round(sm_ry * FACTOR)
                        rz_sdk = round(sm_rz * FACTOR)
                        
                        # CRITICAL: Must send MotionCtrl_2 AND EndPoseCtrl together every frame
                        try:
                            # move_spd_rate_ctrl at 40 for firmware-level smoothing
                            piper.MotionCtrl_2(0x01, 0x00, 40, 0x00)
                            piper.EndPoseCtrl(x_sdk, y_sdk, z_sdk, rx_sdk, ry_sdk, rz_sdk)
                            print(f"d[{dx_mm:+.1f}, {dy_mm:+.1f}, {dz_mm:+.1f}]mm | SDK: X={x_sdk} Y={y_sdk} Z={z_sdk} RX={rx_sdk} RY={ry_sdk} RZ={rz_sdk}   ", end="\r")
                        except Exception as e:
                            if not error_printed:
                                print("\n--- SDK COMMAND ERROR ---")
                                print(f"Arguments: X:{x_sdk}, Y:{y_sdk}, Z:{z_sdk}, RX:{rx_sdk}, RY:{ry_sdk}, RZ:{rz_sdk}")
                                print(f"Error: {repr(e)}")
                                print("-------------------------\n")
                                error_printed = True
                                
                        # Visual Telemetry HUD
                        active_ids = getattr(tracker, 'active_marker_ids', [])
                        grip_str = "OPEN (70mm)" if gripper_is_open else "CLOSED (Grasp)"
                        grip_col = (0, 255, 0) if gripper_is_open else (0, 165, 255)
                        
                        cv2.putText(frame, "STATUS: ACTIVE", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(frame, f"Robot: X:{sm_x:.0f} Y:{sm_y:.0f} Z:{sm_z:.0f} mm", (10, 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
                        cv2.putText(frame, f"Orientation: RX:{sm_rx:.1f} RY:{sm_ry:.1f} RZ:{sm_rz:.1f} deg", (10, 90), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 255, 200), 1)
                        cv2.putText(frame, f"Tracked Markers: {active_ids}", (10, 120), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                        cv2.putText(frame, f"Gripper: {grip_str}", (10, 150), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, grip_col, 2)
                        cv2.putText(frame, "Press SPACE/'c': Gripper | 's': Pause | 'q': Quit", (10, frame.shape[0] - 20), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
                    else:
                        cv2.putText(frame, "STATUS: WAITING FOR ORIGIN", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                        cv2.putText(frame, "Press 'o' to SET ORIGIN", (10, 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                else:
                    cv2.putText(frame, "STATUS: MARKER LOST", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                cv2.imshow("Piper-X Relative Teleoperation", frame)
            
            # Throttle to ~100Hz (matching official demo's 0.01s sleep)
            elapsed = time.time() - start_time
            if elapsed < 0.01:
                time.sleep(0.01 - elapsed)

    except KeyboardInterrupt:
        print("\nCaught KeyboardInterrupt, initiating shutdown...")
    except Exception as e:
        print(f"\nRuntime error encountered: {e}")
    finally:
        print("Stopping vision tracker...")
        tracker.stop()
        cv2.destroyAllWindows()
        
        print("Disabling Piper arm...")
        try:
            piper.DisablePiper()
        except Exception:
            try:
                piper.DisableArm(7)
            except:
                pass
            
        print("Teleoperation gracefully terminated.")

if __name__ == "__main__":
    main()