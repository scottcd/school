using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Data.Sqlite;

namespace TerriblePizzaWebApplication.Data {
    public class UserAccount {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Password { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
        public string? CreditCard { get; set; }
        public decimal TotalMoney { get; set; }
        public int TotalPizzas { get; set; }
        public UserAccount() { }
        public UserAccount(int id, string username, string password, string name, string email, string creditCard, int pizzas, int money) {
            Id = id;
            Username = username;
            Password = password;
            Name = name;
            Email = email;
            CreditCard = creditCard;
            TotalMoney = money;
            TotalPizzas = pizzas;
        }

        public void AddTotalPizzasOrdered(int numberOfPizzas) {
            TotalPizzas += numberOfPizzas;
        }
        public void AddTotalMoneySpent(decimal totalSpent) {
            TotalMoney += totalSpent;
        }
    }
}
