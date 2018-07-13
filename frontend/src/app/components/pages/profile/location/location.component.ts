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
}
