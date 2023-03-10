using System;
using Tesseract;

var engine = new TesseractEngine("./tessdata", "eng", EngineMode.Default);
using (var img = Pix.LoadFromFile("./example.png"))
{
    using (var page = engine.Process(img))
    {
        var text = page.GetText();
        Console.WriteLine(text);
    }
}