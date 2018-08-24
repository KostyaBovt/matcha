import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../../../../services/profile.service';

@Component({
  selector: 'app-modify',
  templateUrl: './modify.component.html',
  styleUrls: ['./modify.component.css']
})
export class ModifyComponent implements OnInit {
  username: string;
  fname: string;
  sname: string;
  gender: number;
  sex_preference: number;
  birth: string;
  bio: string;
  phone: string;
  email: string;
  interests: string;
  gender_list: Array<any> =  [
	  {value: 0, name: ""},
	  {value: 1, name: "Male"},
	  {value: 2, name: "Female"},
  ];

  prefer_list: Array<any> =  [
	  {value: 0, name: ""},
	  {value: 1, name: "Male"},
	  {value: 2, name: "Female"},
	  {value: 3, name: "Both"},
  ];

  infoUpdated: number = 0;

  password: string;
  new_password: string;
  repeat_password: string;

  passwordUpdated: number = 0;
  emailConfirmSent: number = 0;

  active: Object = {};
  errors_info: Object = {};
  errors_password: Object = {};
  errors_email: Object = {};

  constructor(private profileService: ProfileService) { }

  private calucateAge(dateString) {
    var today = new Date();
         var birthDate = new Date(dateString);
         var age = today.getFullYear() - birthDate.getFullYear();
         var m = today.getMonth() - birthDate.getMonth();
         if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
              age--;
         }
         return age;
  }

  private formatDateToString(date) {
      let day = date.getDate();
      if (day < 10 ) {
        day = "0" + day;
      }
      let monthIndex = date.getMonth() + 1;
      if (monthIndex < 10) {
        monthIndex = "0" + monthIndex;
      }
      let year = date.getFullYear();
      return year + '-' + monthIndex + '-' + day;
  }

  ngOnInit() {
    this.active['username'] = 0;
    this.active['fname'] = 0;
    this.active['sname'] = 0;
    this.active['birth'] = 0;
    this.active['bio'] = 0;
    this.active['interests'] = 0;

    this.active['email'] = 0;

    this.active['password'] = 0;
    this.active['new_password'] = 0;
    this.active['repeat_password'] = 0;

    this.profileService.get().subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];
            console.log(result);
            this.username = result['username'];
            this.fname = result['fname'];
            this.sname = result['sname'];
            this.gender = result['gender'];
            this.sex_preference = result['sex_preference'];
            this.email = result['email'];
            this.phone = result['phone'];
            this.bio = result['bio'];
            this.interests = result['interests'];
            this.birth = this.formatDateToString(new Date(result['birth']));
        }
    });
  }

  updateInfo() {
    this.infoUpdated = 0;
    this.profileService.update(this.username, this.fname, this.sname, this.gender, this.sex_preference, this.birth, this.phone, this.bio, this.interests).subscribe(response => {
        if (response['success'] == 1) {
            this.infoUpdated = 1;
            this.errors_info = {};
        } else {
            this.infoUpdated = 2;
            if (response['errors']) {
              this.errors_info = response['errors'];
            }
        }
    });
  }

  updatePassword() {
    this.passwordUpdated = 0;
    this.profileService.updatePassword(this.password, this.new_password, this.repeat_password).subscribe(response => {
        if (response['success'] == 1) {
            this.passwordUpdated = 1;
            this.password = "";
            this.new_password = "";
            this.repeat_password = "";
            this.errors_password = {};
        } else {
            if (response['errors']) {
              this.errors_password = response['errors'];
            }
            this.passwordUpdated = 2;
        }
    });
  }

  updateEmail() {
    this.emailConfirmSent = 0;
    this.profileService.updateEmail(this.email).subscribe(response => {
        if (response['success'] == 1) {
            this.emailConfirmSent = 1;
            this.errors_email = {};
        } else {
            if (response['errors']) {
              this.errors_email = response['errors'];
            }
            this.emailConfirmSent = 2;
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
