import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  email: string;
  username: string;
  fname: string;
  sname: string;
  password: string;
  registered: string;

  constructor(public userService: UserService) { }

  ngOnInit() {
    this.registered = '';
  }

  register() {
    this.userService.register(this.username, this.fname, this.sname, this.email, this.password).subscribe(response => {
      if (response['success'] == 1) {
        this.email = "";
        this.username = "";
        this.fname = "";
        this.sname = "";
        this.password = "";
        this.registered = 'Please confirm registration via email!';
      } else {
        this.registered = 'Failed! try again';
      }
    });
  }

}
