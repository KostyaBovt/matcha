import { Component, OnInit } from '@angular/core';
import { NotificationsService } from '../../../services/notifications.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.css']
})
export class NotificationsComponent implements OnInit {

  page: number = 1;
  notifications: Array<any> = [];

  constructor(private notificationsService: NotificationsService) { }

  ngOnInit() {
    this.notificationsService.getList(this.page).subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];

            this.notifications = result['notifications'];
            console.log(this.notifications);
        }
    });
  }

}
