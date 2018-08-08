import { Component, OnInit, OnDestroy } from '@angular/core';
import {Router, ActivatedRoute, Params} from '@angular/router';
import { MessageService } from '../../../services/message.service';
import { ExploreService } from '../../../services/explore.service';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css'],
})
export class MessagesComponent implements OnInit, OnDestroy {

  currentMateId: number = null;
  mateList: Array<any> =[];
  currentMateChat: Array<any> = [];
  messageInput: string = "";
  firstMsgId = 0;

  account_info: Object = {};
  current_main_photo: string = '';

  timeoutId: number = null;

  constructor(private activatedRoute: ActivatedRoute, private messageService: MessageService, private exploreService: ExploreService) { }

  ngOnInit() {

  	let that = this;
  	this.activatedRoute.params.subscribe((params: Params) => {
        that.currentMateId = params['mate_id'];

        if (that.timeoutId) {
        	console.log('clear timeout with id:' + that.timeoutId)
	        clearTimeout(that.timeoutId);
        }

		that.messageService.getMateList().subscribe(response => {
			let result = response['result'];
			console.log(response);
			that.mateList = result['mate_list'];
		});

		if (that.currentMateId) {
		    that.exploreService.getMate(that.currentMateId).subscribe(response => {
		        if (response['success'] == 1) {
		            console.log(response);
		            this.account_info = response['result'];
		            this.current_main_photo = this.account_info['avatar']['src'];
		        } else {
		          alert('some error');
		        }
		    });

			that.messageService.getCurrentMateChat(that.currentMateId).subscribe(response => {
				console.log(response);
				let result = response['result'];
				if (response['success'] == 1) {
					if (result['messages']) {
						that.currentMateChat = result['messages'];
					}
				} else {
					alert('some error!');
				}
			});

		}

		that.timeoutId = setTimeout(function updateMessages() {
        	console.log('new timeout with id:' + that.timeoutId)
			console.log('alert 1 sec');
			


			that.messageService.getCurrentMateChat(that.currentMateId).subscribe(response => {
				console.log(response);
				let result = response['result'];
				if (response['success'] == 1) {
					if (result['messages']) {
						that.currentMateChat = result['messages'];
					} else {
						that.currentMateChat = [];
					}
				} else {
					alert('some error!');
				}
			});


			that.timeoutId = setTimeout(updateMessages, 2000);
		}, 2000);

    });

  }


 	sendMsg() {
	    if (this.currentMateChat.length > 0) {
	    	this.firstMsgId = this.currentMateChat[0]['id'];
	    }

		this.messageService.sendMsg(this.currentMateId, this.messageInput, this.firstMsgId).subscribe(response => {
			let result = response['result'];
			console.log(result);
			this.currentMateChat = this.currentMateChat.concat(result['new_messages']); 
			console.log(this.currentMateChat);
			this.messageInput = '';
		});
	}

	ngOnDestroy() {
        if (this.timeoutId) {
        	console.log('clear timeout with id:' + this.timeoutId)
	        clearTimeout(this.timeoutId);
        }
	}

}
