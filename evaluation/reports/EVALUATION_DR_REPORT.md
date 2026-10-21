======================================================================================
IN-HAND MANIPULATION SIM-TO-REAL DOMAIN RANDOMIZATION REPORT (@10.0% Tol)
Checkpoint: models/best_model_with_dr.pth
Total Episodes Evaluated: 6
DR Conditions:
  • Actuation Delay: 0 to 1 steps (0 to 20 ms lag)
  • ArUco Vision Latency: 1 to 2 steps (20 to 40 ms camera+pose lag)
  • Action Smoothing Filter Alpha: 0.50
  • Observation Sensor Noise Scale: 0.80
  • Fingertip/Palm Silicone Friction: μ in [2.1, 3.9]
  • Object Geometry / Mass / Friction: ±30%
  • Ground-Truth Physical Privileges: Disabled (Nominal Observation Only)
======================================================================================

######################################################################################
SECTION 1: RANGE 1 (10.0° to 40.0° Small-to-Medium Rotations under DR)
######################################################################################
Object       | Episodes | Success   | Closure   | Pre-Ret   | Pre-Drop  | Raw-Drop  | Final Err  | Steps 
---------------------------------------------------------------------------------------------------------
Cylinder     | 1        |  100.0%  |  100.0%  |  100.0%  |    0.0%  |    0.0%  |   3.5°     |  93.0
Cube         | 1        |  100.0%  |  100.0%  |  100.0%  |    0.0%  |    0.0%  |   2.9°     |  31.0
Cuboid       | 1        |  100.0%  |  100.0%  |  100.0%  |    0.0%  |    0.0%  |   2.2°     | 184.0
---------------------------------------------------------------------------------------------------------
RANGE 1 TOTAL | 3        |  100.0%  |  100.0%  |  100.0%  |    0.0%  |    0.0%  |   2.8°     | 102.7
  --> Range 1 Effective Manipulation Index (EMI): 1.0000 | Benchmark Score: 1.0000

######################################################################################
SECTION 2: RANGE 2 (40.0° to 90.0° Large-Angle In-Hand Gaiting under DR)
######################################################################################
Object       | Episodes | Success   | Closure   | Pre-Ret   | Pre-Drop  | Raw-Drop  | Final Err  | Steps 
---------------------------------------------------------------------------------------------------------
Cylinder     | 1        |  100.0%  |  100.0%  |  100.0%  |    0.0%  |    0.0%  |   5.5°     |  78.0
Cube         | 1        |    0.0%  |    0.0%  |    0.0%  |  100.0%  |  100.0%  | 105.5°     | 544.0
Cuboid       | 1        |    0.0%  |    0.0%  |    0.0%  |  100.0%  |  100.0%  | 174.3°     | 305.0
---------------------------------------------------------------------------------------------------------
RANGE 2 TOTAL | 3        |   33.3%  |   33.3%  |   33.3%  |   66.7%  |   66.7%  |  95.1°     | 309.0
  --> Range 2 Effective Manipulation Index (EMI): 0.1111 | Benchmark Score: 0.3333

======================================================================================
SECTION 3: GRAND COMPOSITE SIM-TO-REAL DR SUMMARY (FULL 10° TO 90° ENVELOPE)
======================================================================================
Evaluation Metric                   | Range 1 (10°-40°)    | Range 2 (40°-90°)    | Grand Total    
------------------------------------------------------------------------------------------------
Total Evaluated Episodes            | 3                    | 3                    | 6              
Success Rate (@10.0% Error)         | 100.0              % | 33.3               % | 66.7          %
Mean Rotational Closure             | 100.0              % | 33.3               % | 66.7          %
Pre-Goal Retention Rate             | 100.0              % | 33.3               % | 66.7          %
Pre-Goal Drop Rate                  | 0.0                % | 66.7               % | 33.3          %
Raw Drop Rate (All Steps)           | 0.0                % | 66.7               % | 33.3          %
Mean Final Geodesic Error           | 2.8                ° | 95.1               ° | 49.0          °
Mean Steps per Episode              | 102.7                | 309.0                | 205.8          
Peak Hardware Torque                | 3.95             N·m | 4.16             N·m | 4.16        N·m
Effective Manipulation Index (EMI)  | 1.0000               | 0.1111               | 0.4444         
Composite Benchmark Score           | 1.0000               | 0.3333               | 0.6667         
================================================================================================

