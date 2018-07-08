import { ApiService } from './api.service'
import { Injectable } from '@angular/core';

@Injectable()
export class ProfileService {

  constructor(private apiService: ApiService) { }

  get() {
	return this.apiService.request('profile/get', {});
  }

  update(
  	username: string,
	fname: string,
	sname: string,
	gender: number,
	sex_preference: number,
	birth: string,
	phone: string,
	bio: string,
	interests: string
  ) {
  	let args = {
  		'username': username,
		'fname': fname,
		'sname': sname,
		'gender': gender,
		'sex_preference': sex_preference,
		'birth': birth,
		'phone': phone,
		'bio': bio,
		'interests': interests
  	}
  	return this.apiService.request('profile/update', args)
  }

  updatePassword(
  	password: string,
	new_password: string,
	repeate_password: string
  ) {
  	let args = {
  		'password': password,
		'new_password': new_password,
		'repeate_password': repeate_password
  	}
  	return this.apiService.request('profile/update_password', args)
  }

  updateEmail(
	 new_email: string
  ) {
  	let args = {
  		'new_email': new_email,
  	}
  	return this.apiService.request('profile/update_email', args)
  }

  uploadPhoto(
    photoName: string,
    photoType: string,
    photoValue: string
  ) {
    let args = {
      'photoName': photoName,
      'photoType': photoType,
      'photoValue': photoValue
    }
    return this.apiService.request('profile/upload_photo', args)
  }

  getProfilePhotos() {
    let args = {}
    return this.apiService.request('profile/get_profile_photos', args)
  }

  setAvatar(photo_hash) {
    let args = {'photo_hash': photo_hash}
    return this.apiService.request('profile/set_avatar', args)
  }

  deletePhoto(photo_hash) {
    let args = {'photo_hash': photo_hash}
    return this.apiService.request('profile/delete_photo', args)
  }

}

