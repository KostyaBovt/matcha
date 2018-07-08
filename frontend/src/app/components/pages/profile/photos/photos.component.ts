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
    this.loadPhotos();
  }

  loadPhotos() {
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
            this.loadPhotos();
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

 updateAvatarInArray(photo_hash) {
  this.photos.forEach(function(element) {
    if (element.hash == photo_hash) {
      element.avatar = 1;
    } else {
      element.avatar = 0;
    }
  });
 }

  setAvatar(photo_hash) {
    this.profileService.setAvatar(photo_hash).subscribe(response => {
        if (response['success'] == 1) {
            this.updateAvatarInArray(photo_hash);
        } else {
            alert('Error');
        }
    });
  }


 deletePhotoFromArray(photo_hash) {
  for (var i = this.photos.length - 1; i >= 0; i--) {
    if (this.photos[i].hash == photo_hash) {
      this.photos.splice(i, 1);
    }
  }
 }

  isAvatar(photo_hash) {
    for (var i = 0; i <= this.photos.length - 1; i++) {
      if (this.photos[i].hash == photo_hash && this.photos[i].avatar == 1) {
        return true;
      }
      if (i == this.photos.length - 1) {
        return false;
      }
    }
  }

  getNewFirstAvatarHash() {
    for (var i = 0; i <= this.photos.length - 1; i++) {
      if (this.photos[i].avatar == 0) {
        return this.photos[i].hash;
      }
      if (i == this.photos.length - 1) {
        return this.photos[i].hash;
      }
    }
  }

  deletePhoto(photo_hash) {
    this.profileService.deletePhoto(photo_hash).subscribe(response => {
        if (response['success'] == 1) {
          if (this.isAvatar(photo_hash) && this.photos.length > 1) {
            let newAvatarHash = this.getNewFirstAvatarHash();
            this.profileService.setAvatar(newAvatarHash).subscribe(response => {
                if (response['success'] == 1) {
                    this.updateAvatarInArray(newAvatarHash);
                } else {
                    alert('Error');
                }
            });
          }
          this.deletePhotoFromArray(photo_hash);
        } else {
            alert('Error');
        }
    });
  }


}
