import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {

  constructor(public userService: UserService, private router: Router) { }

  ngOnInit() {
    this.userService.isLoggedIn = false;
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

}
