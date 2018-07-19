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
  	this.profileService.get().subscribe(response => {

  		if (response['success'] == 1 && response['result']['geo_type'] == 1) {
  			// if we get profile data geo_type is 1 (auto)

  			if ("geolocation" in navigator) {
  				let that = this;
  				// if geolocation is supported by browser
  				navigator.geolocation.getCurrentPosition(
  					function success(position) {
  						// if browser rturn geolocation
  						let lat = position.coords.latitude;
  						let lng =  position.coords.longitude;
  						alert("now we will update geolocation:" + lat + ", " + lng);
  						that.profileService.updateCoords(lat, lng).subscribe(response => {
					        if (response['success'] == 1) {
					        } else {
					            alert('error! cant update coordinates');
					        }
					    });
  					},
  					function error(error_message) {
  						// if user deniad geolocation in browser
  						alert('user denied geolocation');
  						that.getIP().subscribe(response => {
  							let IP_adress = response['ip'];
  							that.getLocationByIP(IP_adress).subscribe(response => {
  								let lat = response['lat'];
  								let lng = response['lon'];
		  						that.profileService.updateCoords(lat, lng).subscribe(response => {
							        if (response['success'] == 1) {
							        } else {
							            alert('error! cant update coordinates');
							        }
							    });
  							});
  						});
  					}
  				);
  			} else {
  				// if broser does not support geolocation
  				alert('broeser doesnt suport geolocatio');

  			}


  		} else {
  			// if we cannot get profiele data
  			alert('geolocation is set to manual');
  		}

  	});

  }

  OnInit() {
  }

  getLocationByIP(IP_adress) {
    return this.http.get('http://ip-api.com/json/' + IP_adress);
  }

  getIP() {
    return this.http.get('https://api.ipify.org?format=json');
  }


}
