import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProfileService } from '../../../services/profile.service';
import { ExploreService } from '../../../services/explore.service';

@Component({
  selector: 'app-explore',
  templateUrl: './explore.component.html',
  styleUrls: ['./explore.component.css']
})
export class ExploreComponent implements OnInit {
  man: boolean = false;
  woman: boolean = false;

  bottomAge: number = 18;
  upperAge: number = 100;

  bottomRating: number = 0;
  upperRating: number = 100;

  interests: string;
  radius: number = 50;

  sort_list: Array<any> =  [
	  {value: "match", name: "Match"},
	  {value: "rating", name: "Rating"},
	  {value: "dist", name: "Distance"},
	  {value: "age", name: "Age"},
  ];

  sort: string = "match";
  sex_preference: number;
  age: number;

  constructor(private http: HttpClient, private profileService: ProfileService, private exploreService: ExploreService) { }

  ngOnInit() {
    this.profileService.get().subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];

            this.sex_preference = result['sex_preference'];
            if (this.sex_preference == 1) {
            	this.man = true;
            } else if (this.sex_preference == 2) {
            	this.woman = true;
            } else {
            	this.man = true;
            	this.woman = true;            	
            }

            this.interests = result['interests'];

            this.age = this.calucateAge(result['birth']);
            this.bottomAge = (this.age - 3) < 18 ? 18 : (this.age - 3);
            this.upperAge = (this.age + 3) > 100 ? 100 : (this.age + 3);

        }
    });
  }

  setBottomAge(bottomAge) {
  	this.bottomAge = bottomAge;
  }

  setUpperAge(upperAge) {
  	this.upperAge = upperAge;
  }

  setBottomRating(bottomRating) {
  	this.bottomRating = bottomRating;
  }

  setUpperRating(upperRating) {
  	this.upperRating = upperRating;
  }

  setRadius(radius) {
  	this.radius = radius;
  }

  searchMates() {
  	let args = {
		'man': this.man,
		'woman': this.woman,
		'bottomAge': this.bottomAge,
		'upperAge': this.upperAge,
		'bottomRating': this.bottomRating,
		'upperRating': this.upperRating,
		'interests': this.interests,
		'radius': this.radius,
		'sort': this.sort,
  	}
    this.exploreService.searchMates(args).subscribe(response => {
        if (response['success'] == 1) {
            console.log(response);
        } else {
        	alert('some error');
        }
    });
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

}
