import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProfileService } from '../../../services/profile.service';
import { ExploreService } from '../../../services/explore.service';

@Component({
  selector: 'app-connections',
  templateUrl: './connections.component.html',
  styleUrls: ['./connections.component.css']
})
export class ConnectionsComponent implements OnInit {
  man: boolean = true;
  woman: boolean = true;
  online: boolean = false;
  connections_flag: boolean = true;
  i_like_flag: boolean = false;
  like_me_flag: boolean = false;
  i_dislike_flag: boolean = false;

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

  constructor(private http: HttpClient, private profileService: ProfileService, private exploreService: ExploreService) { }

  ngOnInit() {
    this.profileService.get().subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];

            // this.sex_preference = result['sex_preference'];
            // if (this.sex_preference == 1) {
            // 	this.man = true;
            // } else if (this.sex_preference == 2) {
            // 	this.woman = true;
            // } else {
            // 	this.man = true;
            // 	this.woman = true;            	
            // }

            this.interests = result['interests'];

            // this.age = this.calucateAge(result['birth']);
            // this.bottomAge = (this.age - 3) < 18 ? 18 : (this.age - 3);
            // this.upperAge = (this.age + 3) > 100 ? 100 : (this.age + 3);

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

  searchConnectionsInitial() {
    this.page = 1;
    this.searchConnections(); 
  }

  searchConnections() {
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
		'connections_flag': this.connections_flag,
		'i_like_flag': this.i_like_flag,
		'i_dislike_flag': this.i_dislike_flag,
		'like_me_flag': this.like_me_flag,
	    'page': this.page,
	    'online': this.online
  	}
    this.exploreService.searchConnections(args).subscribe(response => {
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
          this.searchConnections();
        } else {
          alert('some error');
        }
    });
  }
 
  unlike(mate_id) {
    this.exploreService.unlike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          this.searchConnections();
        } else {
          alert('some error');
        }
    });
  }

  dislike(mate_id) {
    this.exploreService.dislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          this.searchConnections();
        } else {
          alert('some error');
        }
    });
  }

  undislike(mate_id) {
    this.exploreService.undislike(mate_id).subscribe(response => {
        if (response['success'] == 1) {
          this.searchConnections();
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
    this.searchConnections();
  }

  prevPage() {
    this.page = this.page - 1;
    this.searchConnections();
  }

	manageConnectionsFlagChange() {
		if (!this.connections_flag) {
	  		this.connections_flag = true;
	  		this.i_like_flag = false;
	  		this.like_me_flag = false;
	  		this.i_dislike_flag = false;
		}
	}

	manageILikeFlagChange() {
		if (!this.i_like_flag) {
	  		this.connections_flag = false;
	  		this.i_like_flag = true;
	  		this.like_me_flag = false;
	  		this.i_dislike_flag = false;
		}
	}

	manageLikeMeFlagChange() {
		if (!this.like_me_flag) {
	  		this.connections_flag = false;
	  		this.i_like_flag = false;
	  		this.like_me_flag = true;
	  		this.i_dislike_flag = false;
		}
	}

	manageIDisikeFlagChange() {
		if (!this.i_dislike_flag) {
	  		this.connections_flag = false;
	  		this.i_like_flag = false;
	  		this.like_me_flag = false;
	  		this.i_dislike_flag = true;
		}
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
    this.searchConnections();
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
    alert('no we go to messages');
  }
}
