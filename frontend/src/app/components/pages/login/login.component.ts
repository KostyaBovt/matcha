import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  username: string;
  password: string;
  message: string;

  constructor(public userService: UserService, private router: Router) { }

  ngOnInit() {
    let redir = this.userService.redirectUrl;

    if (this.userService.checkLoggedIn()) {
      if (redir) {
        this.router.navigate([redir]);
        this.userService.redirectUrl = ''
      } else {
        this.router.navigate(['/explore']);
      }
    }

    let token = localStorage.getItem('token');
    if (token) {
      this.userService.auth(token).subscribe(response => {
          if (response['success'] ==1) {
            this.userService.isLoggedIn = true;

            if (redir) {
              this.router.navigate([redir]);
              this.userService.redirectUrl = ''
            } else {
              this.router.navigate(['/explore']);
            }

          }
        }
      );
      
    }
  }

  login() {
    this.message = '';
    this.userService.login(this.username, this.password).subscribe(response => {
      if (response['success'] == 1) {
        this.username = "";
        this.password = "";
        this.message = "";
        localStorage.setItem('token', response['token']);
        this.userService.isLoggedIn = true;
        this.router.navigate(['/explore']);
      } else {
        this.message = 'Login Failed! try again';
      }
    });
  }
}
