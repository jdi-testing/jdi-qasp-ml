import {Component} from '@angular/core';
import {FormGroup, FormControl} from '@angular/forms';

/** @title Date range picker forms integration */
@Component({
  selector: 'app-datepicker-forms',
  templateUrl: './datepicker-forms.component.html',
  styleUrls: ['./datepicker-forms.component.css']
})
export class DatepickerFormsComponent {
  range = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });
}
