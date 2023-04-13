def web_page(pwm_pin):
    print(pwm_pin)
    print('duty..................................')
    html = """<!DOCTYPE HTML><html><head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
                <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
                    h2 { font-size: 3.0rem; } p { font-size: 3.0rem; } .units { font-size: 1.2rem; } 
                    .ds-labels{ font-size: 1.5rem; vertical-align:middle; padding-bottom: 15px; }
                </style></head><body>
                <div class="container">
                    <div class="row">
                        <div class="col-sm">
                            left
                        </div>
                        <div class="col-sm">
                            right
                        </div>
                        <div class="col-sm">
                            up
                        </div>
                        <div class="col-sm">
                            down
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm">
                            <p>Motor Speed: <strong>""" + str(pwm_pin.duty()) + """</strong></p>
                                <form action="/" method="POST">
                                <input type="number" name="motor_speed" min="0" max="1000" value="0">
                                <input type="submit" value="Update Motor">

                                <div id="div1"></div>
                                </form>
                                <button class="up">up</button>
                                <button class="down">down</button>
                    </div>
                </div>
                <script>

                    $(".up").click(function(){
                        $.ajax({url: "?motor_speed=""" + str(pwm_pin.duty() + 5) + """", success: function(result){
                            $(".up").html(result);
                        }});
                    });
                    $(".down").click(function(){
                        $.ajax({url: "?motor_speed=""" + str(pwm_pin.duty() - 5) + """", success: function(result){
                            $(".down").html(result);
                        }});
                    });
                </script>
                </body></html>"""
    return html