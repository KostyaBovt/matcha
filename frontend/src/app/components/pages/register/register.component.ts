import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  login: string;
  password: string;
  registered: string;

  constructor(public userService: UserService) { }

  ngOnInit() {
    this.registered = 'not registered';
  }

  register() {
  	this.userService.register(this.login, this.password).subscribe(response => {
      if (response['success'] == 'true') {
        this.registered = 'register success';
      } else {
        this.registered = 'register fail';
      }
      console.log(response);
    });
  }

}
