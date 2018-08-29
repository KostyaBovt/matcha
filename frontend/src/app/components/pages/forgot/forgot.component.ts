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
  loading: number = 0;

  errors: Object = {};

  constructor(public userService: UserService) { }

  ngOnInit() {
    this.sended = '';
  }

  sendForgot() {
  	this.sended = 'Sending reset password email';
    this.loading = 1;
    this.userService.sendForgot(this.email).subscribe(response => {
      if (response['success'] == 1) {
        this.sended = 'Check you email to reset password';
        this.email = '';
        this.errors = {};
        this.loading = 0;
      } else {
        this.errors = response['errors'];
        this.sended = 'Something went wrong...Check the email.';
        this.loading = 0;
      }
    });
  }
}