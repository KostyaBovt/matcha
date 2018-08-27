import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ProfileService } from '../../../services/profile.service';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Component({
    templateUrl: './main.component.html',
    styleUrls: ['./main.component.css']
})

export class MainComponent {
	geo_lat: number;
	geo_lng: number;	
	geo_type: number;
	myIP: string;


  constructor(private profileService: ProfileService, private http: HttpClient) {

  }

  ngOnInit() {
    // console.log('init main');
  	this.profileService.get().subscribe(response => {



			// if we get profile data geo_type is 1 (auto)
      if (response['success'] == 1 && response['result']['geo_type'] == 1) {

				let that = this;
        if ("geolocation" in navigator) {
  				// if geolocation is supported by browser
  				navigator.geolocation.getCurrentPosition(
  					function(position) {
  						// if browser rturn geolocation
  						let lat = position.coords.latitude;
  						let lng =  position.coords.longitude;
              that.profileService.updateCoords(lat, lng).subscribe(response => {
                  if (response['success'] == 1) {
        						// console.log("main comp: get from browser and update db:" + lat + ", " + lng);
					        } else {
					            // console.log('error! cant update coordinates');
					        }
					    });
  					},
  					function(error_message) {
  						// if user deniad geolocation in browser
  						// console.log('user denied geolocation');
  						that.getIP().subscribe(response => {
  							let IP_adress = response['ip'];
  							that.getLocationByIP(IP_adress).subscribe(response => {
  								let lat = response['lat'];
  								let lng = response['lon'];
		  						that.profileService.updateCoords(lat, lng).subscribe(response => {
							        if (response['success'] == 1) {
							        } else {
							            // console.log('error! cant update coordinates');
							        }
							    });
  							});
  						});
  					}
  				);
  			} else {
  				// if broser does not support geolocation
  				// console.log('browser doesnt suport geolocation');
            that.getIP().subscribe(response => {
              let IP_adress = response['ip'];
              that.getLocationByIP(IP_adress).subscribe(response => {
                let lat = response['lat'];
                let lng = response['lon'];
                that.profileService.updateCoords(lat, lng).subscribe(response => {
                    if (response['success'] == 1) {
                    } else {
                        // console.log('error! cant update coordinates');
                    }
                });
              });
            });

  			}


  		} else {
  			// if we cannot get profiele data or geotype is manual
  			// console.log('geolocation is set to manual or cant get user');
      }

  	});


  }

  getLocationByIP(IP_adress) {
    return this.http.get('http://ip-api.com/json/' + IP_adress);
  }

  getIP() {
    return this.http.get('https://api.ipify.org?format=json');
  }


}
