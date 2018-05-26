import {Injectable}       from '@angular/core';
import {
    CanActivate,
    Router,
    ActivatedRouteSnapshot,
    RouterStateSnapshot
}                           from '@angular/router';
import {Subject, Observable} from "rxjs";
import {Response} from "@angular/http";

@Injectable()
export class AuthGuard implements CanActivate {

    constructor(private router: Router) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        
        // this.router.navigate(['/login']);
        return true;
    }
}
