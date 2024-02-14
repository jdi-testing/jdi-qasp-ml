import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-button-toggle',
  templateUrl: './button-toggle.component.html',
  styleUrls: ['./button-toggle.component.css']
})
export class ButtonToggleComponent implements OnInit {
  @Input() type?: number;

  constructor() { }

  ngOnInit(): void {
  }

}
