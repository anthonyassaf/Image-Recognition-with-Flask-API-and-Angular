import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FaceExpressionComponent } from './face-expression/face-expression.component';
import { FaceMaskComponent } from './face-mask/face-mask.component';
import { GenderClassificationComponent } from './gender-classification/gender-classification.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [  
  { path: 'home', component: HomeComponent},
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'gender', component: GenderClassificationComponent },
  { path: 'expressions', component: FaceExpressionComponent },
  { path: 'mask', component: FaceMaskComponent },
  { path: '**', component: HomeComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
