import { Component, OnInit } from '@angular/core';
import { NotificationsService } from '../../../services/notifications.service';
import { ExploreService } from '../../../services/explore.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.css']
})
export class NotificationsComponent implements OnInit {

  page: number = 1;
  notifications: Array<any> = [];
  account_shown: boolean = false;
  account_shown_id: number = null;
  account_info: Object = {};
  current_main_photo: string = '';

  constructor(private notificationsService: NotificationsService, private exploreService: ExploreService) { }

  ngOnInit() {
  	this.searchNotifications();
  }

  searchNotifications() {
    this.notificationsService.getList(this.page).subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];
            // console.log(result['notifications']);
            if (result['notifications'] == null) {
            	this.notifications = [];
            } else {
	            this.notifications = result['notifications'];
            }
        }
    });
  }

  nextPage() {
  	this.page = this.page + 1;
  	this.searchNotifications();
  }

  prevPage() {
  	this.page = this.page - 1;
  	this.searchNotifications();
  }

  showAccount(mate_id) {
    this.exploreService.getMate(mate_id, 1).subscribe(response => {
        if (response['success'] == 1) {
            // console.log(response);
            this.account_shown = true;
            this.account_shown_id = mate_id;
            this.account_info = response['result'];
            this.current_main_photo = this.account_info['avatar']['src'];
        } else {
          alert('some error');
        }
    });
  }

  changeMainPhoto(src) {
    this.current_main_photo = src;
  }

  closeAccount() {
    this.account_shown = false;
    this.account_shown_id = null;
    this.account_info = {};
  }

  likeFromAccount(mate_id) {
    this.exploreService.like(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          // console.log(response);
          this.updateActions(1, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  unlikeFromAccount(mate_id) {
    this.exploreService.unlike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          // console.log(response);
          this.updateActions(null, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  dislikeFromAccount(mate_id) {
    this.exploreService.dislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          // console.log(response);
          this.updateActions(2, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  undislikeFromAccount(mate_id) {
    this.exploreService.undislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          // console.log(response);
          this.updateActions(null, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  reportFromAccount(mate_id) {
    if (!confirm("you really wnat to report this user? you will not able to conntact him/her anymore!")) {
    } else {
      this.exploreService.report(mate_id).subscribe(response => {
          if (response['success'] == 1) {
            // console.log(response);
            this.updateActions(3, response['result']['action_to_user']);
          } else {
            alert('some error');
          }
      });
    }
  }

  updateActions(action_of_user, action_to_user) {
    this.account_info['action_of_user'] = action_of_user;
    this.account_info['action_to_user'] = action_to_user;
  }

  goToMessages(mate_id) {
    alert('no we go to messages')
  }

}
