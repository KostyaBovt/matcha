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
  repeate_password: string;

  passwordUpdated: number = 0;
  emailConfirmSent: number = 0;

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

  ngOnInit() {
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
            this.birth = result['birth'];
        }
    });
  }

  updateInfo() {
    this.profileService.update(this.username, this.fname, this.sname, this.gender, this.sex_preference, this.birth, this.phone, this.bio, this.interests).subscribe(response => {
        if (response['success'] == 1) {
            this.infoUpdated = 1;
        } else {
            this.infoUpdated = 2;
        }
    });
  }

  updatePassword() {
    this.profileService.updatePassword(this.password, this.new_password, this.repeate_password).subscribe(response => {
        if (response['success'] == 1) {
            this.passwordUpdated = 1;
        } else {
            this.passwordUpdated = 2;
        }
    });
  }

  updateEmail() {
    this.profileService.updateEmail(this.email).subscribe(response => {
        if (response['success'] == 1) {
            this.emailConfirmSent = 1;
        } else {
            this.emailConfirmSent = 2;
        }
    });
  }

}
