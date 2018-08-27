import { Component, OnInit, OnDestroy  } from '@angular/core';
import { NotificationsService } from '../../../services/notifications.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy {

  notifCount: Object = {'new_notif': 0, 'new_msg': 0};
  timeoutId: number = 0;

  constructor( private notificationsService: NotificationsService) { }

  ngOnInit() {

    let that = this;
    this.timeoutId = setTimeout(function updateNotifCount() {
      // console.log('new timeout with id:' + that.timeoutId)
      // console.log('alert 1 sec');

      that.notificationsService.getNotifCount().subscribe(response => {
        // console.log(response);

        if (response['success'] == 1) {
          let result = response['result']
          that.notifCount['new_msg'] = result['new_msg'];
          that.notifCount['new_notif'] = result['new_notif'];
        } else {
          // alert('some error');
        }

      });


      that.timeoutId = setTimeout(updateNotifCount, 2000);
    }, 2000);

  }

  ngOnDestroy() {
        if (this.timeoutId) {
          // console.log('clear timeout with id:' + this.timeoutId)
          clearTimeout(this.timeoutId);
        }
  }


}
