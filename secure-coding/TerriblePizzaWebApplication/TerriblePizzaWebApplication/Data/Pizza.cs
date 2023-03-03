using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Data.Sqlite;

namespace TerriblePizzaWebApplication.Data {
    public class Pizza {
        public int Id{ get; set; }
        public string Name { get; set; }
        public int Price { get; set; }
        public string Sauce { get; set; }
        public string Topping1 { get; set; }
        public string? Topping2 { get; set; }
        public string? Topping3 { get; set; }
        public Pizza() { }
        public Pizza(int id, string name, int price, string sauce, string topping1, string topping2, string topping3) {
            Id = id;
            Name = name;
            Price = price;
            Sauce = sauce;
            Topping1 = topping1;
            Topping2 = topping2;
            Topping3 = topping3;
        }
    }
}
