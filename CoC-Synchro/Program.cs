// See https://aka.ms/new-console-template for more information

//using IronOcr;
//var Ocr = new IronTesseract();
//using (var Input = new OcrInput("image.png"))
//{
//	// Input.Deskew();  // use if image not straight
//	// Input.DeNoise(); // use if image contains digital noise
//	var Result = Ocr.Read(Input);
//	Console.WriteLine(Result.Text);
//}

using System;
using System.Drawing;
using Tesseract;

var engine = new TesseractEngine("./tessdata", "eng", EngineMode.Default);
using (var img = Pix.LoadFromFile("image.png"))
{
	using (var page = engine.Process(img))
	{
		var text = page.GetText();
		Console.WriteLine(text);
	}
}

Console.WriteLine("Hello, World!");
