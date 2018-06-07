import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-reset',
  templateUrl: './reset.component.html',
  styleUrls: ['./reset.component.css']
})
export class ResetComponent implements OnInit {
  email_hash: string;
  reset_hash: string;
  password: string;
  repeat_password: string;
  is_allowed: boolean = false;
  message: string = "";

  constructor(private route: ActivatedRoute, private userService: UserService) {
  }

  ngOnInit() {
  	this.email_hash = this.route.snapshot.params['email_hash'];
  	this.reset_hash = this.route.snapshot.params['reset_hash'];

  	this.userService.checkReset(this.email_hash, this.reset_hash).subscribe(response => {
  		if (response['success'] == 1) {
  			this.is_allowed = true;
  		} else {
  			this.message = 'Something went wrong. Please check you email for reset link.';
  		}
  	})
  }

  reset() {
    this.userService.reset(this.email_hash, this.reset_hash, this.password, this.repeat_password).subscribe(response => {
      if (response['success'] == 1) {
        this.password = "";
        this.repeat_password = "";
        this.message = 'Your password was updated';
      } else {
        this.message = 'Failed! try again';
      }
    });
  }

}
