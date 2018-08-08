import { Component, OnInit } from '@angular/core';
import {Router, ActivatedRoute, Params} from '@angular/router';
import { MessageService } from '../../../services/message.service';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css'],
})
export class MessagesComponent implements OnInit {

  currentMateId: number = null;
  mateList: Array<any> =[];
  currentMateChat: Array<any> = [];
  messageInput: string = "";
  firstMsgId = 0;

  constructor(private activatedRoute: ActivatedRoute, private messageService: MessageService) { }

  ngOnInit() {

  	let that = this;
  	this.activatedRoute.params.subscribe((params: Params) => {
        that.currentMateId = params['mate_id'];

		that.messageService.getMateList().subscribe(response => {
			let result = response['result'];
			that.mateList = result['mate_list'];
		});

		if (that.currentMateId) {
			that.messageService.getCurrentMateChat(that.currentMateId).subscribe(response => {
				console.log(response);
				let result = response['result'];
				if (response['success'] == 1) {
					that.currentMateChat = result['messages'];
					console.log(that.currentMateChat);
				} else {
					alert('some error!');
				}
			});
		}

		// if (that.currentMateId) {
  //       	setTimeout(function doSomething() {
		//     	console.log("1 seconds");
		//     	that.sendMsg();
		//     	setTimeout(doSomething,1000);
		// 	}, 1000);
		// }

    });

  }


  // updateMessages() {
  // 		this.messageService.getMessages().subscribe(response => {
  // 			let result = response['result'];
  // 			this.sideMates = result['side_mates'];
  // 		);
  // 		setTimeout(this.updateMessages, 10000);
  // }



  clearAllTimeouts() {
  	var id = window.setTimeout(function() {}, 0);
	while (id--) {
		window.clearTimeout(id);
	}
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
		});
	}

}
