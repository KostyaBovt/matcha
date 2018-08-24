import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-forgot',
  templateUrl: './forgot.component.html',
  styleUrls: ['./forgot.component.css']
})
export class ForgotComponent implements OnInit {
  sended: string;
  email: string;

  errors: Object = {};

  constructor(public userService: UserService) { }

  ngOnInit() {
    this.sended = '';
  }

  sendForgot() {
  	this.sended = 'Sending reset password email'
    this.userService.sendForgot(this.email).subscribe(response => {
      if (response['success'] == 1) {
        this.sended = 'Check you email to reset password';
        this.email = '';
        this.errors = {};
      } else {
        this.errors = response['errors'];
        this.sended = 'Something went wrong...Check the email.';
      }
    });
  }
}