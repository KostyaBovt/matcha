import { Injectable } from '@angular/core';
import { CanActivate, Router,  ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Subject, Observable } from "rxjs";
import { Response } from "@angular/http";
import { UserService } from './user.service';

@Injectable()
export class AuthGuard implements CanActivate {
    token: string;

    constructor(private router: Router, private userService: UserService) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | boolean {
        
        this.token = localStorage.getItem('token')
        
        if (!this.token) {
            this.userService.redirectUrl = state.url;
            this.router.navigate(['/login']);
            return false;
        }
        
        if (!this.userService.checkLoggedIn()) {
            this.userService.redirectUrl = state.url;
            this.router.navigate(['/login']);
            return false;
        }

        return true;       
    }
}
