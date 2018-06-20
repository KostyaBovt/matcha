import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-modify',
  templateUrl: './modify.component.html',
  styleUrls: ['./modify.component.css']
})
export class ModifyComponent implements OnInit {
  username: string = 'iguana';
  fname: string = 'kostya';
  sname: string = 'bovt';
  gender: number = 1;
  sex_preference: number = 2;
  birth: string = '1994-12-16';
  bio: string = 'thi is some info about my person';
  phone: string = '+380997741343';
  email: string = 'kostya.bovt@gmail.com';
  interests: string = 'football, swimming, science, food';
  gender_list: Array<any> =  [
	  {value: 0, name: ""},
	  {value: 1, name: "Male"},
	  {value: 2, name: "Female"},
	  {value: 3, name: "Other"},
  ];

  prefer_list: Array<any> =  [
	  {value: 0, name: ""},
	  {value: 1, name: "Male"},
	  {value: 2, name: "Female"},
	  {value: 3, name: "Both"},
  ];

  constructor() { }

  ngOnInit() {
  }

}
