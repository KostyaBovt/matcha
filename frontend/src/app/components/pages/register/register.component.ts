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

  active: Object = {};
  errors: Object = {};

  constructor(public userService: UserService) { }

  ngOnInit() {
    this.registered = '';
    this.active['email'] = 0;
    this.active['username'] = 0;
    this.active['fname'] = 0;
    this.active['sname'] = 0;
    this.active['password'] = 0;
  }

  register() {
    this.registered = "";
    this.userService.register(this.username, this.fname, this.sname, this.email, this.password).subscribe(response => {
      if (response['success'] == 1) {
        this.errors = {};
        this.email = "";
        this.username = "";
        this.fname = "";
        this.sname = "";
        this.password = "";
        this.registered = 'Please confirm registration via email!';
      } else {
        this.errors = response['errors'];
        this.registered = 'Failed! try again';
      }
    });
  }

  onFocus(event) {
    this.active[event.target.name] = 1;
  }

  onFocusOut(event) {
    this.active[event.target.name] = 0;
  }

}
