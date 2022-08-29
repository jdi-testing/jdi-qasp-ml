import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-expansion-panel',
  templateUrl: './expansion-panel.component.html',
  styleUrls: ['./expansion-panel.component.css']
})
export class ExpansionPanelComponent implements OnInit {
  @Input() type?: number;

  constructor() { }

  ngOnInit(): void {
  }

}