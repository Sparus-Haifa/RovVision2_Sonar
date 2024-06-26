# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
topic_sitl_position_report=b'position_rep'
topic_sitl_position_report_port=7755

topic_thrusters_comand=b'thruster_cmd'
#opration modes
topic_system_state=b'system_state'

topic_controller_port = topic_thrusters_comand_port=7788
thrusters_sink_port = 7787
topic_lights=b'topic_lights'
topic_focus=b'topic_set_focus_state'
topic_tracker_cmd=b'topic_tracker_start_stop_cmd'



topic_check_thrusters_comand=b'thruster_check_cmd'
topic_check_thrusters_comand_port=9005

topic_autoFocus_port = 7790
topic_autoFocus = b'autoFocus'

#cameta control topics
topic_cam_toggle_auto_exp  = b'auto_exposureCam'
topic_cam_toggle_auto_gain = b'auto_gainCam'
topic_cam_inc_exp          = b'inc_exposureCam'
topic_cam_dec_exp          = b'dec_exposureCam'
topic_cam_exp_val          = b'exp_value'
topic_cam_ctrl_port = 7791

#topic_camera_left=b'topic_camera_left'
#topic_camera_right=b'topic_camera_right'
topic_stereo_camera    = b'topic_stereo_camera'
topic_stereo_camera_ts = b'topic_stereo_camera_ts'

topic_camera_port=7789

topic_button = b'joy_button'
topic_axes   = b'joy_axes'
topic_hat    = b'joy_hat'
topic_joy_port=8899

topic_gui_controller       = b'gui_controller'
topic_gui_diveModes        = b'gui_diveModes'
topic_gui_focus_controller = b'manual_focus'
topic_gui_depthAtt         = b'att_depth'
topic_gui_autoFocus        = b'auto_focus'
topic_gui_start_stop_track = b'tracker_cmd'
topic_gui_toggle_auto_exp  = b'auto_exposureCmd'
topic_gui_inc_exp          = b'inc_exposureCmd'
topic_gui_dec_exp          = b'dec_exposureCmd'
topic_gui_exposureVal      = b'exposureValue'
topic_gui_toggle_auto_gain = b'auto_gainCmd'

topic_gui_update_pids      = b'updatePIDS'

topic_gui_port = 8900

topic_motors_output = b'motors_output'
topic_motors_output_port = 8898


#diffrent topics due to difrent freq devices
topic_imu = b'topic_imu'
topic_imu_port = 8897

topic_sonar = b'topic_sonar'
topic_sonar_port = 9304

topic_depth = b'topic_depth'
topic_depth_port = 9302

#messages:
#stop/start recording

topic_record_state=b'record_state'
topic_record_state_port=9303

topic_local_route_port=9995

topic_viewer_data=b'topic_viewer_data'

topic_depth_hold_pid=b'topic_depth_control'
topic_depth_hold_port=9997
topic_att_hold_yaw_pid=b'topic_att_yaw_control'
topic_att_hold_pitch_pid=b'topic_att_pitch_control'
topic_att_hold_roll_pid=b'topic_att_roll_control'
topic_att_hold_port=10052

topic_imHoldPos_port=10054

topic_pos_hold_pid_fmt=b'topic_pos_hold_pid_%d'
topic_pos_hold_port=10053


topic_tracker        = b'topic_tracker'
topic_tracker_result = b'topic_simple_tracker_result'
topic_tracker_port   = 10101


topic_volt=b'topic_volt'
topic_volt_port=10102

topic_hw_stats=b'topic_hw_stats'
topic_hw_stats_port=10103
