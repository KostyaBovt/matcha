import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../../../../services/profile.service';

@Component({
  selector: 'app-view',
  templateUrl: './view.component.html',
  styleUrls: ['./view.component.css']
})
export class ViewComponent implements OnInit {
	username: string = '';
	fname: string = '';
	sname: string = '';
	gender: string = '';
	sex_preference: string = '';
	email: string = '';
	phone: string = '';
	bio: string = '';
	age: number;

  constructor(private profileService: ProfileService) { }

  private getGender(code) {
	let gender = '';
	switch (code) {
	  case 1:
	    gender = 'Male';
	    break;
	  case 2:
	    gender = 'Female';
	    break;
	  case 3:
	    gender = 'Other';
	    break;
	  default:
	    gender = 'Not specified';
	}
	return gender;
  }

  private getSexPreference(code) {
	let sex_preference = '';
	switch (code) {
	  case 1:
	    sex_preference = 'Male';
	    break;
	  case 2:
	    sex_preference = 'Female';
	    break;
	  case 3:
	    sex_preference = 'Both';
	    break;
	  default:
	    sex_preference = 'Not specified';
	}
	return sex_preference;
  }

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
			this.gender = this.getGender(result['gender']);
			this.sex_preference = this.getSexPreference(result['sex_preference']);
			this.email = result['email'];
			this.phone = result['phone'];
			this.bio = result['bio'];
			if (result['birth']) {
				this.age = this.calucateAge(result['birth'])
			}
  		}
  	});
  }

}
