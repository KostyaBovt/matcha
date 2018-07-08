import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { ProfileService } from '../../../../services/profile.service';

@Component({
  selector: 'app-photos',
  templateUrl: './photos.component.html',
  styleUrls: ['./photos.component.css']
})
export class PhotosComponent implements OnInit {
  photoName: string = "some_photo_name";
  photoType: string = "some_photo_type";
  photoValue: string = "some_photo_value";
  photoUploaded : number = 0;

  photos: Array<any>;

  @ViewChild('fileInput') fileInput: ElementRef;

  constructor(private profileService: ProfileService) { }

  ngOnInit() {
    this.profileService.getProfilePhotos().subscribe(response => {
      if (response['success'] == 1) {
        this.photos = response['photos'];
      }
    });
  }

  uploadPhoto() {
    this.profileService.uploadPhoto(this.photoName, this.photoType, this.photoValue).subscribe(response => {
        if (response['success'] == 1) {
            this.photoUploaded = 1;
        } else {
            this.photoUploaded = 2;
        }
    });
  }

  onFileChange(event) {
    let reader = new FileReader();
    if(event.target.files && event.target.files.length > 0) {
      let file = event.target.files[0];
      reader.readAsDataURL(file);
      reader.onload = () => {
      	this.photoName = file.name;
      	this.photoType = file.type;
      	this.photoValue = reader.result.split(',')[1];
      };
    }
  }

}
