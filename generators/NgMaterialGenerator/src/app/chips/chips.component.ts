import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-chips',
  templateUrl: './chips.component.html',
  styleUrls: ['./chips.component.css']
})
export class ChipsComponent implements OnInit {
  @Input() type?: number;

  constructor() { }

  ngOnInit(): void {
  }

}
