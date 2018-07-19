import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../../../../services/profile.service';

@Component({
  selector: 'app-location',
  templateUrl: './location.component.html',
  styleUrls: ['./location.component.css']
})
export class LocationComponent implements OnInit {
  geo_type: number;
  geo_lat: number = 50.4317;
  geo_lng: number = 30.5163;
  geo_lat_marker: number = 50.43179;
  geo_lng_marker: number = 30.51639;
  geotype_list: Array<any> =  [
	  {value: 1, name: "Auto"},
	  {value: 2, name: "Manual"},
  ];


  constructor(private profileService: ProfileService) {
  }

  ngOnInit() {
    this.profileService.get().subscribe(response => {
        if (response['success'] == 1) {
            let result = response['result'];
        	this.geo_type = result['geo_type'];
        	this.geo_lat = result['geo_lat'];
        	this.geo_lng = result['geo_lng'];
        } else {
            alert('error! not updated');
        }
    });
  }

  updateGeotype() {
    this.profileService.updateGeotype(this.geo_type).subscribe(response => {
        if (response['success'] == 1) {
        } else {
            alert('error! not updated');
        }
    });
  }

  updateCoords() {
    this.profileService.updateCoords(this.geo_lat_marker, this.geo_lng_marker).subscribe(response => {
        if (response['success'] == 1) {
        } else {
            alert('error! not updated');
        }
    });
  }

  onChooseLocation(event) {
    this.profileService.updateCoords(event.coords.lat, event.coords.lng).subscribe(response => {
        if (response['success'] == 1) {
          this.geo_lat = event.coords.lat;
          this.geo_lng = event.coords.lng;
          this.geo_lat_marker = event.coords.lat;
          this.geo_lng_marker = event.coords.lng;
        } else {
            alert('error! not updated');
        }
    });
  }

}
