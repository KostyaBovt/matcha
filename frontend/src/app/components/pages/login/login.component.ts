import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
  some_text : string = "ssssssss";

  constructor() { }

  ngOnInit() {
  }

  alert1() {
  	this.some_text = 'ALERT!!!';
  }
}
