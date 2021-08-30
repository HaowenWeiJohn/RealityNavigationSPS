color_pink = '#fff5f6'
color_white = '#ffffff'
color_gray = '#f0f0f0'
color_bright = '#E8E9EB'

button_color = color_white

button_style_classic = "background-color: " + button_color + "; border-style: outset; border-width: 2px; " \
                                                             "border-radius: 10px; " \
                                                             "border-color: gray; font: 12px; min-width: 10em; " \
                                                             "padding: 6px; "

default_theme = 'dark'

inference_button_style = "max_width: 250px;, min_width: 100px; font: bold 14px"
sensors_type_ui_name_dict = {'OpenBCICyton': 'OpenBCI Cyton',
                             # 'RNUnityEyeLSL': 'Vive Pro eye-tracking (Unity)',
                             }

sensor_ui_name_type_dict = {v: k for k, v in sensors_type_ui_name_dict.items()}


default_add_lsl_data_type = 'YourStreamName'

sampling_rate_decimal_places = 2

cam_display_width = 640
cam_display_height = 480

capture_display_width = 640
capture_display_height = 480

progress_bar_updat_freq = 50
######################## indexpen experinment default config #######################
indexpen_interval_default_max = 4
indexpen_repeats_default_max = 10

indexpen_interval_time_default = 4 # in second
indexpen_repeats_num_default = 1

# indexPen_classes_default = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z Spc Bspc Ent Act'
indexPen_classes_default = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z Spc Bspc Ent Act Nois'

# indexPen_classes_default = 'Nois Act T H E Spc F I V E Spc B O X I N G Spc W I Z A R D S Spc J U M P Spc Q U I C K L Y Act Nois'
# indexPen_classes_default = 'Nois Act A Spc L A R G E Spc F A W N Spc J U M P E D Spc Q U I C K L Y Spc O V E R Spc W H I T E Spc Z I N C Spc B O X E S Act Nois'
# indexPen_classes_default = 'Nois Act J A Y Spc V I S I T E D Spc B A C K Spc H O M E Spc A N D Spc G A Z E D Spc U P O N Spc A Spc B R O W N Spc F O X Spc A N D Spc Q U A I L Act Nois'
# indexPen_classes_default = 'Nois Act F I V E Spc O R Spc S I X Spc B I G Spc J E T Spc P L A N E S Spc Z O O M E D Spc Q U I C K L Y Spc B Y Spc T H E Spc T O W E R Act Nois'
# indexPen_classes_default = 'Nois Act T H E Spc Q U I C K Spc B R O W N Spc F O X Spc J U M P S Spc O V E R Spc T H E Spc L A Z Y Spc D O G Act Nois'

marker_lsl_outlet_name_default = 'IndexPen-30'
error_marker_lsl_outlet_name_default = 'IndexPen-30-Error'
