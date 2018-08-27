import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../../../../services/profile.service';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-location',
  templateUrl: './location.component.html',
  styleUrls: ['./location.component.css']
})
export class LocationComponent implements OnInit {
  geo_type: number;
  geo_lat: number;
  geo_lng: number;
  geo_lat_marker: number;
  geo_lng_marker: number;
  geotype_list: Array<any> =  [
	  {value: 1, name: "Auto"},
	  {value: 2, name: "Manual"},
  ];
  markerUploaded: boolean = false;


  constructor(private profileService: ProfileService, private http: HttpClient) {
  }

  ngOnInit() {
    console.log('init location');

    // need this just only to get curent location again after we done this in main component
    this.profileService.get().subscribe(response => {

      if (response['success'] == 1 && response['result']['geo_type'] == 1) {
          this.geo_type = response['result']['geo_type'];
        // if we get profile data geo_type is 1 (auto)

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
                    that.geo_lat = lat;
                    that.geo_lng = lng;
                    that.geo_lat_marker = lat;
                    that.geo_lng_marker = lng;
                    that.markerUploaded = true;
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
                  that.geo_lat = lat;
                  that.geo_lng = lng;
                  that.geo_lat_marker = lat;
                  that.geo_lng_marker = lng;
                  that.markerUploaded = true;
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
          // console.log('broeser doesnt suport geolocatio');
            that.getIP().subscribe(response => {
              let IP_adress = response['ip'];
              that.getLocationByIP(IP_adress).subscribe(response => {
                let lat = response['lat'];
                let lng = response['lon'];
                that.geo_lat = lat;
                that.geo_lng = lng;
                that.geo_lat_marker = lat;
                that.geo_lng_marker = lng;
                that.markerUploaded = true;
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
        // if we cannot get profiele data or geo-type is manual
        // console.log('geolocation is set to manual');
        let result = response['result'];
        this.geo_type = result['geo_type'];
        this.geo_lat = parseFloat(result['geo_lat']);
        this.geo_lng = parseFloat(result['geo_lng']);
        this.geo_lat_marker = parseFloat(result['geo_lat']);
        this.geo_lng_marker = parseFloat(result['geo_lng']);
        this.markerUploaded = true;
      }

    });

  }

  updateGeotype() {
    this.profileService.updateGeotype(this.geo_type).subscribe(response => {
        if (response['success'] == 1) {
          if (this.geo_type == 1) {
            // there we must update uatomaticaly geolocation

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
                        that.geo_lat = lat;
                        that.geo_lng = lng;
                        that.geo_lat_marker = lat;
                        that.geo_lng_marker = lng;
                        that.markerUploaded = true;
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
                      that.geo_lat = lat;
                      that.geo_lng = lng;
                      that.geo_lat_marker = lat;
                      that.geo_lng_marker = lng;
                      that.markerUploaded = true;
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
              // console.log('broeser doesnt suport geolocatio');
                that.getIP().subscribe(response => {
                  let IP_adress = response['ip'];
                  that.getLocationByIP(IP_adress).subscribe(response => {
                    let lat = response['lat'];
                    let lng = response['lon'];
                    that.geo_lat = lat;
                    that.geo_lng = lng;
                    that.geo_lat_marker = lat;
                    that.geo_lng_marker = lng;
                    that.markerUploaded = true;
                    that.profileService.updateCoords(lat, lng).subscribe(response => {
                        if (response['success'] == 1) {
                        } else {
                            // console.log('error! cant update coordinates');
                        }
                    });
                  });
                });
            }

          }
        } else {
            // console.log('error! not updated');
        }
    });
  }

  updateCoords() {
    this.profileService.updateCoords(this.geo_lat_marker, this.geo_lng_marker).subscribe(response => {
        if (response['success'] == 1) {
        } else {
            // console.log('error! not updated');
        }
    });
  }

  onChooseLocation(event) {
    if (this.geo_type != 2) {
      return;
    }
    this.profileService.updateCoords(event.coords.lat, event.coords.lng).subscribe(response => {
        if (response['success'] == 1) {
          this.geo_lat = event.coords.lat;
          this.geo_lng = event.coords.lng;
          this.geo_lat_marker = event.coords.lat;
          this.geo_lng_marker = event.coords.lng;
        } else {
            // console.log('error! not updated');
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
