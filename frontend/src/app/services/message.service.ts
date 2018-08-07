import { Injectable } from '@angular/core';
import { ApiService } from './api.service'

@Injectable()
export class MessageService {

  constructor(private apiService: ApiService) { }

  getMateList() {
  	let args = {};
    return this.apiService.request('messages/get_mate_list', args);
  }

  getCurrentMateChat(mate_id) {
  	let args = {'mate_id': mate_id};
    return this.apiService.request('messages/get_current_mate_chat', args);
  }

  sendMsg(mate_id, message) {
  	let args = {'mate_id': mate_id, 'message': message};
    return this.apiService.request('messages/send_msg', args);
  }


}
