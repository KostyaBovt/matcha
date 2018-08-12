import { ApiService } from './api.service'
import { Injectable } from '@angular/core';

@Injectable()
export class NotificationsService {

  constructor(private apiService: ApiService) { }

  getList(page) {
  	let args = {'page': page};
    return this.apiService.request('notifications/get_list', args);
  }

  getNotifCount() {
  	let args = {};
    return this.apiService.request('notifications/get_notif_count', args);
  }

}
