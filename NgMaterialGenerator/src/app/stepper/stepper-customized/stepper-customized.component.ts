
import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {STEPPER_GLOBAL_OPTIONS} from '@angular/cdk/stepper';

/**
 * @title Stepper with customized states
 */
 @Component({
  selector: 'app-stepper-customized',
  templateUrl: './stepper-customized.component.html',
  styleUrls: ['./stepper-customized.component.css']
})
export class StepperCustomizedComponent implements OnInit {
// @ts-ignore
  firstFormGroup: FormGroup;
  // @ts-ignore
  secondFormGroup: FormGroup;

  constructor(private _formBuilder: FormBuilder) {}

  ngOnInit() {
    this.firstFormGroup = this._formBuilder.group({
      firstCtrl: ['', Validators.required]
    });
    this.secondFormGroup = this._formBuilder.group({
      secondCtrl: ['', Validators.required]
    });
  }
}
