import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-confirm',
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.css']
})
export class ConfirmComponent implements OnInit {

  email_hash: string;
  confirm_hash: string;
  message: string = "Waiting for confirmation";
  is_confirmed: boolean = false;

  constructor(private route: ActivatedRoute, private userService: UserService) {
  }

  ngOnInit() {
  	this.email_hash = this.route.snapshot.params['email_hash'];
  	this.confirm_hash = this.route.snapshot.params['confirm_hash'];

  	this.userService.confirm(this.email_hash, this.confirm_hash).subscribe(response => {
  		if (response['success'] == 1) {
  			this.message = 'Account is activated! You can log in!';
  			this.is_confirmed = true;
  		} else {
  			this.message = 'Something went wrong. Please check you email for confirmation link.';
  		}
  	});
  }

}
