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
	gender: number;
	sex_preferences: number;
	email: string = '';
	phone: string = '';
	bio: string = '';

  constructor(private profileService: ProfileService) { }

  ngOnInit() {
  	this.profileService.get().subscribe(response => {
  		if (response['success'] == 1) {
  			let result = response['result'];
  			console.log(result);
			this.username = result['username'];
			this.fname = result['fname'];
			this.sname = result['sname'];
			this.gender = result['gender'];
			this.sex_preferences = result['sex_preferences'];
			this.email = result['email'];
			this.phone = result['phone'];
			this.bio = result['bio'];
  		}
  	});
  }

}
