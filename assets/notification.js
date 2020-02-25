 function my_special_notification_callback(data){
                unread_count = data['unread_count'];
                if (unread_count == 0){
                    unread_count = '';
                }
                $('.live_notify_badge').text();
            }