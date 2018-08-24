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
  online: boolean = false;

  bottomAge: number = 18;
  upperAge: number = 100;

  bottomRating: number = 0;
  upperRating: number = 100;

  interests: string;
  radius: number = 50;

  sort_list: Array<any> =  [
    {value: "match_desc", name: "Match", order: "desc"},
    {value: "match_asc", name: "Match", order: "asc"},
    {value: "age_desc", name: "Age", order: "desc"},
    {value: "age_asc", name: "Age", order: "asc"},
    {value: "rating_desc", name: "Rating", order: "desc"},
    {value: "rating_asc", name: "Rating", order: "asc"},
    {value: "dist_desc", name: "Distance", order: "desc"},
    {value: "dist_asc", name: "Distance", order: "asc"},
  ];

  sort: string= "match_desc";
  sex_preference: number;
  age: number;

  page: number = 1;

  finded_mates: Array<any> = [];

  account_shown: boolean = false;
  account_shown_id: number = null;
  account_info: Object = {};
  current_main_photo: string = '';

  filled: number = 2;
  avatar: number = 1;


  constructor(private http: HttpClient, private profileService: ProfileService, private exploreService: ExploreService) { }

  ngOnInit() {
    this.profileService.get().subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];
            console.log(result);
            this.filled = result['filled'];
            if (!result['avatar']) {
              this.avatar = 0;
            }


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

  searchMatesInitial() {
    this.page = 1;
    this.searchMates(); 
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
    'page': this.page,
    'online': this.online
  	}
    this.exploreService.searchMates(args).subscribe(response => {
        if (response['success'] == 1) {
            console.log(response);
            this.finded_mates = response['result'];
            if (response['result'] == null) {
              this.finded_mates = [];
            }
        } else {
        	alert('some error');
        }
    });
  }

  like(mate_id) {
    this.exploreService.like(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          this.searchMates();
        } else {
          alert('some error');
        }
    });
  }

  dislike(mate_id) {
    this.exploreService.dislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          this.searchMates();
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

  nextPage() {
    this.page = this.page + 1;
    this.searchMates();
  }

  prevPage() {
    this.page = this.page - 1;
    this.searchMates();
  }

////////// ############### this part is for mate account view

  showAccount(mate_id) {
    this.exploreService.getMate(mate_id, 1).subscribe(response => {
        if (response['success'] == 1) {
            console.log(response);
            this.account_shown = true;
            this.account_shown_id = mate_id;
            this.account_info = response['result'];
            this.current_main_photo = this.account_info['avatar']['src'];
        } else {
          alert('some error');
        }
    });
  }

  changeMainPhoto(src) {
    this.current_main_photo = src;
  }

  closeAccount() {
    this.account_shown = false;
    this.account_shown_id = null;
    this.account_info = {};
    this.searchMates();
  }

  likeFromAccount(mate_id) {
    this.exploreService.like(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          console.log(response);
          this.updateActions(1, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  unlikeFromAccount(mate_id) {
    this.exploreService.unlike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          console.log(response);
          this.updateActions(null, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  dislikeFromAccount(mate_id) {
    this.exploreService.dislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          console.log(response);
          this.updateActions(2, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  undislikeFromAccount(mate_id) {
    this.exploreService.undislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          console.log(response);
          this.updateActions(null, response['result']['action_to_user']);
        } else {
          alert('some error');
        }
    });
  }

  reportFromAccount(mate_id) {
    if (!confirm("you really wnat to report this user? you will not able to conntact him/her anymore!")) {
    } else {
      this.exploreService.report(mate_id).subscribe(response => {
          if (response['success'] == 1) {
            console.log(response);
            this.updateActions(3, response['result']['action_to_user']);
          } else {
            alert('some error');
          }
      });
    }
  }

  updateActions(action_of_user, action_to_user) {
    this.account_info['action_of_user'] = action_of_user;
    this.account_info['action_to_user'] = action_to_user;
  }

  goToMessages(mate_id) {
    alert('no we go to messages')
  }
}
