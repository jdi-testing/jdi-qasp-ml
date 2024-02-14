import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-bottom-sheet',
  templateUrl: './bottom-sheet.component.html',
  styleUrls: ['./bottom-sheet.component.css']
})
export class BottomSheetComponent implements OnInit {
  @Input() type?: number;

  constructor() { }

  ngOnInit(): void {
  }

}
