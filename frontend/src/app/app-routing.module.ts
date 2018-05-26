import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {AuthGuard} from './services/auth-guard.service';


import { ExploreComponent } from './components/pages/explore/explore.component';
import { ProfileComponent } from './components/pages/profile/profile.component';
import { MessagesComponent } from './components/pages/messages/messages.component';
import { ConnectionsComponent } from './components/pages/connections/connections.component';
import { NotificationsComponent } from './components/pages/notifications/notifications.component';
import {MainComponent} from './components/layout/layout/main.component';
import {BlankComponent} from './components/layout/layout/blank.component';
import {LoginComponent} from './components/pages/login/login.component';
import {PageNotFoundComponent} from './components/pages/pagenotfound/pagenotfound.component';
import { RegisterComponent } from './components/pages/register/register.component';
import { ForgotComponent } from './components/pages/forgot/forgot.component';
import { ResetComponent } from './components/pages/reset/reset.component';


export const blankLayoutRoutes: Routes = [
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: 'forgot',
        component: ForgotComponent
    },
    {
        path: 'reset',
        component: ResetComponent
    },
    {
        path: 'register',
        component: RegisterComponent
    },
];

export const mainLayoutRoutes: Routes = [
	{ path: 'explore', component: ExploreComponent, canActivate: [AuthGuard] },
	{ path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
	{ path: 'messages', component: MessagesComponent, canActivate: [AuthGuard] },
	{ path: 'connections', component: ConnectionsComponent, canActivate: [AuthGuard] },
	{ path: 'notifications', component: NotificationsComponent, canActivate: [AuthGuard] },
    { path: '**', component: PageNotFoundComponent, canActivate: [AuthGuard] }
];

const routes: Routes = [
    { path: '', redirectTo: '/explore', pathMatch: 'full' },
    { path: '', component: BlankComponent, children: blankLayoutRoutes },
    { path: '', component: MainComponent, children: mainLayoutRoutes }

];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}