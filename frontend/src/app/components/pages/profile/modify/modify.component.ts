import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-modify',
  templateUrl: './modify.component.html',
  styleUrls: ['./modify.component.css']
})
export class ModifyComponent implements OnInit {
  username: string = '';
  genders: Array<any> =  ["", "Male", "Female", "Other"];

  constructor() { }

  ngOnInit() {
  }

}
