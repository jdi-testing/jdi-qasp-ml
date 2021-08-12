import {Component} from '@angular/core';
import {ThemePalette} from '@angular/material/core';

/**
 * @title Configurable slide-toggle
 */
 @Component({
  selector: 'app-slide',
  templateUrl: './slide.component.html',
  styleUrls: ['./slide.component.css']
})
export class SlideComponent {
  color: ThemePalette = 'accent';
  checked = false;
  disabled = false;
}
